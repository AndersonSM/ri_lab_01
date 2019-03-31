# Recupera��o da Informa��o e Busca na Web
## Laborat�rio 01: Crawlers

### Descri��o

Neste laborat�rio exploraremos o conceito de *Focused Crawler*. Como forma de exerc�cio, buscaremos conte�do de forma automatizada em portais de not�cias. Para tanto, ser� preciso reconhecer o conte�do �til em cada p�gina acessada. Com este objetivo, utilizares um estrat�gia simples baseada no pr�prio layout HTML do site alvo. Felizmente as p�ginas HTML publicadas em portais deste tipo seguem um layout HTML recorrente, o qual pode ser reconhecido de forma autom�tica facilmente. Este ser� o objetivo deste laborat�rio.

Com o intuito de evitar preju�zos quanto � disponibilidade de acesso do site alvo, elencamos seis dom�nios diferentes para serem distribu�dos entre os alunos. Cada dom�nio ser� explorado por doze alunos diferentes de forma independente (sem forma��o de grupos). Seguem os dom�nios poss�veis abaixo;

- brasil247.com
- brasil.elpais.com
- cartacapital.com.br
- diariodocentrodomundo.com.br
- gazetadopovo.com.br
- oantagonista.com

Durante a aula faremos a distribui��o destes dom�nios.

### Objetivos

O objetivo principal � reunir um m�nimo de 100 not�cias posteriores a 01/01/2018 e export�-las para um arquivo CSV conforme *layout* abaixo.

| Campo     | Tipo     | Descri��o                      |
| --------- | -------- | ------------------------------ |
| title     | String   |                                |
| sub_title | String   |                                |
| author    | String   |                                |
| date      | Datetime | dd/mm/yyyy hh:mi:ss            |
| section   | String   | Esportes, Sa�de, Pol�tica, etc |
| text      | String   |                                |
| url       | String   |                                |


Deste modo, pretendemos explorar o conceito de Crawler na pr�tica. Assim sendo, n�o apenas o resultado final ser� avaliado, mas o c�digo. A presen�a de *politeness practices*, a leitura do arquivo *robots.txt*, a verifica��o do *sitemap* ou do *feed* de not�cias ser�o diferenciais.

### O C�digo

O c�digo a seguir j� foi utilizado em projeto do departamento de Computa��o da UFCG, foi testado para todos os portais mencionados e em seguida teve trechos removidos com o intuito de servir a prop�sitos did�ticos. Trata-se de um programa desenvolvido em Python que emprega um *framework* chamado Scrapy. Scrapy � uma crawler de c�digo aberto que prov� o arcabou�o principal deste laborat�rio.

Para compreender este c�digo � necess�rio ler a [documenta��o b�sica](http://docs.scrapy.org/en/latest/intro/tutorial.html) do Scrapy, caso n�o a conhe�a.

O projeto est� dividido em quatro pastas

- frontier
- ri_lab_01
- seeds
- output

A pasta `seeds` traz em arquivo JSON as sementes do algoritmo de *crawling*, ou seja, os links iniciais a serem utilizados pelo seu c�digo. O c�digo opera a partir de c�pias destes arquivos na pasta `frontier`. A pasta `ri_lab_01` traz o projeto em si. Para fins de corre��o, � importante utilizar apenas as sementes disponibilizadas nos arquivos em `seeds`. J� na pasta `output`, consta apenas o arquivo `results.csv`, que est� vazio, mas dever� conter seus resultados.