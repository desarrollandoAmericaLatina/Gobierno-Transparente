#!/bin/sh
#\
exec tclsh "$0" "$@"

package require http
package require htmlparse

load /usr/lib/tcltk/sqlite3/libtclsqlite3.so

source "common.tcl"

interp recursionlimit {} 100000
set current_legislatura 47
#set cuerpo D

proc bajar {fecdesde fechasta} {
  set params [http::formatQuery \
    Asistencia Legislador Cuerpo $::cuerpo \
    FecDesde $fecdesde FecHasta $fechasta \
    Fechas Seleccionado Fin $fechasta \
    IMAGE1 Confirmar Ini 15022010 \
    Legislatura $::current_legislatura \
    Orden ASC]
  set h [http::geturl "http://www0.parlamento.gub.uy/palacio3/abms2/asistsala/ConsAsistencia.asp" -query $params]
  set data [http::data $h]
  http::cleanup $h
  return $data
}

proc guardar {nombre texto} {
  set fd [open $nombre w]
  puts -nonewline $fd $texto
  close $fd
}

#guardar "foo.html" [bajar 23102011 23102011]
#set tree [tree_from_html_file foo.html]

#dump_tree $tree $n

proc parse_asist {tree} {
  set n [findtypes $tree root "body" "table" "tr" "tr"]
  set table {}
  set row {}
  while {$n ne ""} {
    set data ""
    foreach ch [$tree children $n] {
      if {[$tree get $ch type] eq "PCDATA"} {
	append data [string trim [string map {&nbsp; " "} [$tree get $ch data]]]
      }
    }
    set type [$tree get $n type]
    if {$type eq "td"} {
      lappend row $data
    } elseif {$type eq "tr"} {
      lappend table $row
      set row {}
    }
    set n [findtype $tree $n {tr|td}]
  }
  lappend table $row
  return $table
}

#puts [parse_asist $tree]

proc update_asist {table fecha db} {
  global cuerpo
  $db eval {delete from asist where fecha=$fecha and cuerpo=$cuerpo;}
  foreach row $table {
    if {$row eq {}} {continue}
    foreach {nombre citaciones asist asist_per faltca faltca_per faltsa
		faltsa_per licencias pasajes} $row {break}
    $db eval {insert into asist values($fecha, $cuerpo, $nombre, $citaciones, $asist,
		$faltca, $faltsa, $licencias, $pasajes);}
  }
}

proc tomorrow {fecha} {
  set s [clock scan $fecha -format "%d%m%Y"]
  set s [clock add $s 36 hours]
  return [clock format $s -format "%d%m%Y"]
}

proc trabajar {fecha} {
  puts "bajando $fecha..."
  set html [bajar $fecha [tomorrow $fecha]]
  if {[string match {*>0 sesiones*} $html]} {
    puts "0 sesiones"
    return
  }
  puts "procesando $fecha..."
  set tree [struct::tree]
  htmlparse::2tree $html $tree
  set table [parse_asist $tree]
  sqlite3 midb "asist.db"
  update_asist $table $fecha midb
  midb close
  $tree destroy
}

# fecha_fin no incluída!!!
proc trabajar_rango {fecha_init fecha_fin} {
  set fecha $fecha_init
  while {$fecha ne $fecha_fin} {
    trabajar $fecha
    set fecha [tomorrow $fecha]
  }
}

set from 15022010
set to [tomorrow [clock format [clock seconds] -format %d%m%Y]]

foreach {opt value} $argv {
  switch -- $opt {
    -from {
      if {![regexp {^[0-3][0-9][01][0-9]20[0-9][0-9]$} $value]} {
	puts "formato de fecha inválida, ejemplo 27 de julio de 2011: 29072011"
	exit 1
      }
      set from $value
    }
    -to {
      if {![regexp {^[0-3][0-9][01][0-9]20[0-9][0-9]$} $value]} {
	puts "formato de fecha inválida, ejemplo 27 de julio de 2011: 29072011"
	exit 1
      }
      set to $value
    }
    -legislatura {
      # hardcodié el máximo a 99, este valor deberá ser cambiado antes del año 2275.
      if {![string is integer $value] || $value < 45 || $value > 99} {
	puts "Legislatura inválida, debe ser un número mayor o igual a 45."
	puts "45: 2000-2004, 46: 2005-2009, 47: 2010-2014..."
	exit 1
      }
    }
    -cuerpo {
      if {$value ne "D" && $value ne "S"} {
	puts "Cuerpo inválido, solo admitidos D para diputados, y S para senadores."
	exit 1
      }
      set cuerpo $value
    }
    default {
      puts "Syntax: $argv0 \[-from DDMMYYYY\] \[-to DDMMYYY\] \[-legislatura NUM\] -cuerpo (D|S)"
      puts ""
      puts "Con este script se actualizan las asistencias desde la fecha mencionada en -from"
      puts "hasta la fecha en -to (no incluído)."
      exit 1
    }
  }
}

#trabajar_rango 15022010 22102011

if {![info exists cuerpo]} {
  puts "Corra $argv0 con -help para ver como utilizar este proceso."
  exit
}

trabajar_rango $from $to
