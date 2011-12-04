require 'rubygems'
require 'open-uri'
require 'nokogiri'

def parse_td(td_s, partidos, bloque, offset=0)
  foto = "http://www0.parlamento.gub.uy" + td_s[0+offset].css('img').attr('src')
  apellido, nombre = td_s[0+offset].css('img')[0].attr('title').split(", ")
  correo = td_s[2+offset].children.xpath('ul/li/a[contains(text(), "Correo")]').first
  correo = correo.attr('title') unless correo.nil?
  partidos[bloque] << { :foto => foto,
                        :correo => correo,
                        :apellido => apellido,
                        :nombre => nombre,
                        :id => /.*Fot([0-9]+)\.jpg/.match(foto)[1] }
end

def nn(url)
  bloque = nil
  partidos = {}

  doc = Nokogiri::HTML(open(url))

  doc.xpath('//div/center/table[1]/tr').each do |p|
    if (p.css('font[size="3"]').count > 0)
      bloque = p.text.strip
      partidos[bloque] = [] unless partidos.has_key?(bloque)
    else
      unless bloque.nil?
        td_s = p.css('td')
        if td_s[0].css('img').count > 0
          parse_td(td_s, partidos, bloque)
          if td_s.count > 3
            parse_td(td_s, partidos, bloque, 3)
          end
        end
      end
    end
  end
  partidos.each do |key, value|
    partidos.delete(key) if value.empty?
  end
  partidos
end

result = {
  :senador        => nn("http://www0.parlamento.gub.uy/palacio3/legisladores/conozcaasuslegisladores.asp?Cuerpo=S&Legislatura=47&Tipo=T&xWidth="),
  :representante  => nn("http://www0.parlamento.gub.uy/palacio3/legisladores/conozcaasuslegisladores.asp?Cuerpo=D&Legislatura=47&Tipo=T&xWidth=")
}

strings = <<-SQL
  create table datos(
    cargo    varchar(100),
    partido  varchar(100),
    foto     varchar(100),
    correo   varchar(100),
    apellido varchar(100),
    nombre   varchar(100),
    id       varchar(20)
  );
SQL

result.each do |cargo, datos|
  datos.each do |partido, personas|
    personas.each do |persona|
      strings << "insert into datos values('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % [
        cargo,
        partido,
        persona[:foto],
        persona[:correo],
        persona[:apellido],
        persona[:nombre],
        persona[:id]
      ]
    end
  end
end

puts strings
