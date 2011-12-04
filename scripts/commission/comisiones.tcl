#!/bin/sh
#\
exec tclsh "$0" "$@"

package require http

load /usr/lib/tcltk/sqlite3/libtclsqlite3.so

source ../../tcllib/common.tcl

proc bajar {cuerpo} {
  set url "http://www0.parlamento.gub.uy/IndexDB/Distribuidos/DistxComision.asp?Cuerpo=$cuerpo"

  set h [http::geturl $url]
  set html [http::data $h]
  http::cleanup $h
  return $html
}

proc work {cuerpo} {
  set res {}
  set tree [struct::tree]
  htmlparse::2tree [bajar $cuerpo] $tree
  set n [findtype $tree root select]
  foreach ch [$tree children $n] {
    if {[$tree get $ch type] eq "option"} {
      set key [$tree get $ch data]
      set value [lindex [regexp -inline -nocase {value=([0-9]*)} $key] 1]
      if {$value eq ""} {
	error "Error parseando"
      }
      set value [string trimleft $value 0]
      if {$value eq ""} {set value 0}
      lappend res $value
    } else {
      set value [$tree get [findtype $tree $ch PCDATA] data]
      set value [string trim [regsub -all {\(.*?\)} $value ""]]
      lappend res $value
    }
  }
  return $res
}

proc guardar {db cuerpo res} {
  foreach {key value} $res {
    $db eval {
      insert into comisiones(cuerpo, id, nombre)
      values ($cuerpo, $key, $value);
    }
  }
}

set db "comisiones.db"

foreach {opt value} $argv {
  switch -- $opt {
    -db {
      set db $value
    }
    default {
      puts "Syntax: $argv0 \[-db database\]"
      exit 1
    }
  }
}

sqlite3 midb $db
catch {midb eval {drop table comisiones;}}
midb eval {
  create table comisiones(cuerpo, id, nombre);
}
guardar midb D [work D]
guardar midb S [work S]
midb close
