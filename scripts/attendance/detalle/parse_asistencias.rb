require 'net/http'
require 'nokogiri'
require 'pp'
require 'json'

def parse_results(res)
  doc = Nokogiri::HTML(res.body)
  sesiones = []

  a_selector = '//center/a'
  table_selector = '//center/a/following-sibling::table'
  script_selector = '//script[contains(text(), "innerHTML = \'Procesando Sesiones")]'

  doc.xpath(a_selector).zip(doc.xpath(table_selector), doc.xpath(script_selector)).each do |a, table, script|
    fecha = script.text[/[0-9]{2}\/[0-9]{2}\/[0-9]{4}/]
    nro = /Sesi.n ([0-9]+)/.match(a.text)[1]
    diario = if a.attr("href") =~ /pdf$/
              a.attr("href")
             else
               ""
             end
    sesion = { :nro => nro,
               :fecha => fecha,
               :diario => diario }

    ["Con licencia", "Faltan con", "Faltan sin", "Asisten"].each do |tipo_asistencia|
      regexp = /#{tipo_asistencia}[^:]*:([^.]*)\./
      match = regexp.match(table.text)
      asistencias = if match
                      match[1].split(/,|\b y  \b/).map(&:strip).map do |name|
                        if /(.*) \([0-9]+\)$/.match(name)
                          /(.*) \([0-9]+\)$/.match(name)[1]
                        else
                          name
                        end
                      end
                    else
                      []
                    end
      sesion[tipo_asistencia] = asistencias
    end
    sesiones << sesion
  end

  sesiones
end


uri = URI('http://www0.parlamento.gub.uy/palacio3/abms2/asistsala/ConsAsistenciabrief.asp')
datos = { :senadores => [], :representantes => [] }

# senadores 2005/2010
res = Net::HTTP.post_form(uri,
                          'FecDesde' => '15022005',
                          'FecHasta' => '04022010',
                          'Cuerpo' => 'S',
                          'Ini' => '15022005',
                          'Fin' => '04022010',
                          'Legislatura' => '46',
                          'Fechas' => 'Seleccionado',
                          'IMAGE1' => 'Confirmar')
datos[:senadores] << parse_results(res)

# senadores 2010/2015
res = Net::HTTP.post_form(uri,
                          'Cuerpo' => 'S',
                          'FecDesde' => '15022010',
                          'FecHasta' => '30112011',
                          'Fechas' => 'Seleccionado',
                          'Fin' => '30112011',
                          'IMAGE1' => 'Confirmar',
                          'Ini' => '15022010',
                          'Legislatura' => '47')
datos[:senadores] << parse_results(res)

# representantes 2000/2005
res = Net::HTTP.post_form(uri,
                          'FecDesde' => '12122001',
                          'FecHasta' => '15122004',
                          'Cuerpo' => 'D',
                          'Ini' => '12122001',
                          'Fin' => '15122004',
                          'Legislatura' => '45',
                          'Fechas' => 'Seleccionado',
                          'IMAGE1' => 'Confirmar')
datos[:representantes] << parse_results(res)

# representantes 2005/2010
res = Net::HTTP.post_form(uri,
                          'FecDesde' => '15022005',
                          'FecHasta' => '03022010',
                          'Cuerpo' => 'D',
                          'Ini' => '15022005',
                          'Fin' => '03022010',
                          'Legislatura' => '46',
                          'Fechas' => 'Seleccionado',
                          'IMAGE1' => 'Confirmar')
datos[:representantes] << parse_results(res)

# representantes 2010/2015
res = Net::HTTP.post_form(uri,
                          'FecDesde' => '15022010',
                          'FecHasta' => '23102011',
                          'Cuerpo' => 'D',
                          'Ini' => '15022010',
                          'Fin' => '23102011',
                          'Legislatura' => '47',
                          'Fechas' => 'Seleccionado',
                          'IMAGE1' => 'Confirmar')
datos[:representantes] << parse_results(res)


pp datos.to_json
