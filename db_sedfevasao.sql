CREATE TABLE sedfevasao (
        cod_coordenacao_regional VARCHAR(255),
        coordenacao_regional VARCHAR(255),
        cod_escola VARCHAR(255),
        escola VARCHAR(255),
        cod_curso VARCHAR(255),
        curso VARCHAR(255),
        cod_serie VARCHAR(255),
        serie VARCHAR(255),
        cod_turno VARCHAR(255),
        turno VARCHAR(255),
        cod_turma VARCHAR(255),
        turma VARCHAR(255),
        cod_aluno VARCHAR(255),
        situacao VARCHAR(255)
);

COPY sedfevasao(cod_coordenacao_regional, coordenacao_regional, cod_escola, escola, cod_curso, curso, cod_serie, serie, cod_turno, turno, cod_turma, turma, cod_aluno, situacao)
FROM '/tmp/sedfevasao.csv'
DELIMITER ';'
CSV HEADER;

select * from sedfevasao;