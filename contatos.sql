create schema minicursoAEMS;
use minicursoAEMS;
select * from contatos;
truncate table contatos;
drop table contatos;
show tables;


CREATE TABLE contatos(
    id integer AUTO_INCREMENT,
    nome varchar(255),
    celular varchar(255),
    email varchar(255),
     PRIMARY KEY(id) 
);

