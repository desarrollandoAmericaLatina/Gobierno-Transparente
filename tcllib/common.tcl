package require htmlparse
package require struct::tree

proc findtype {tree node type} {
  foreach ch [$tree children $node] {
    if {[regexp "^$type\$" [$tree get $ch type]]} {
      return $ch
    }
    set e [findtype $tree $ch $type]
    if {$e ne ""} {
      return $e
    }
  }
  return ""
}

proc findtypes {tree node args} {
  foreach type $args {
    set node [findtype $tree $node $type]
  }
  return $node
}

proc dump_tree {tree node {margin ""}} {
  set type [$tree get $node type]
  set t "${margin}($type)[string map {"\n" "\\n" "\t" " "} [$tree getall $node]]"
  puts "[string range $t 0 130]"
  foreach ch [$tree children $node] {
    dump_tree $tree $ch "$margin  "
  }
}

proc tree_from_html_file {filename} {
  set fd [open $filename]
  set tree [struct::tree]
  htmlparse::2tree [read $fd] $tree
  close $fd
  return $tree
}
