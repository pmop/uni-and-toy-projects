CREATE TABLE funcionario (
	cod_func INT(10) PRIMARY KEY,
	nome VARCHAR(50),
	dt_nasc INT(10),
	cod_dep INT(10),
	CONSTRAINT fk_cod_dep_departamento FOREIGN KEY (cod_dep) REFERENCES departamento(cod_dep)
);

CREATE TABLE departamento (
	cod_dep INT(10) PRIMARY KEY,
	descr VARCHAR(50),
	localizacao VARCHAR(50)
);

CREATE TABLE projeto (
	cod_proj INT(10) PRIMARY KEY,
	nome VARCHAR(50),
	orcamento DOUBLE,
	data_termino DATE,
	data_prev_termino DATE
);

CREATE TABLE funcao (
	cod_funcao INT(10),
	nome VARCHAR(50),
	salario DOUBLE
);


CREATE TABLE trabalha (
	cod_proj INT(10),
	cod_func INT(10),
	cod_funcao INT(10),
	nome VARCHAR(50),
	orcamento DOUBLE,
	data_termino DATE,
	data_prev_termino DATE,

	CONSTRAINT fk_cod_proj_projeto FOREIGN KEY (cod_proj) REFERENCES projeto(cod_proj),
	CONSTRAINT fk_cod_func_funcionario FOREIGN KEY (cod_func) REFERENCES funcionario(cod_func),
	CONSTRAINT fk_cod_funcao_funcao FOREIGN KEY (cod_funcao) REFERENCES funcao(cod_funcao),
	CONSTRAINT pk_trabalha PRIMARY KEY (cod_proj, cod_func, cod_funcao)
);

