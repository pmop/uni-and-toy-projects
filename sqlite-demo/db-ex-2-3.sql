CREATE TABLE empregado (
    cpf INT(10) PRIMARY KEY,
    pnome VARCHAR(45),
    minicial CHAR(1),
    unome VARCHAR(45),
    datanasc DATETIME,
    endereco VARCHAR(90),
    sexo TEXT CHECK(sexo IN ('M', 'F')),
    salario DOUBLE,
    dnumero INT(10),
    cpf_supervisor INT(10),
    FOREIGN KEY (cpf_supervisor) REFERENCES empregado(cpf),
    FOREIGN KEY (dnumero) REFERENCES departamento(dnumero)
);

CREATE TABLE dependente (
    nome_dependente VARCHAR(45),
    cpf INT(10) NOT NULL,
    sexo TEXT CHECK(sexo IN ('M', 'F')),
    datanasc DATETIME,
    parentesco VARCHAR(30),
    PRIMARY KEY (nome_dependente, cpf),
    FOREIGN KEY (cpf) REFERENCES empregado(cpf)
);

CREATE TABLE departamento (
    dnumero INT(10) PRIMARY KEY,
    dnome VARCHAR(45),
    datainicio_gerente DATETIME,
    cpf_gerente INT(10),
    FOREIGN KEY (cpf_gerente) REFERENCES empregado(cpf)
);

CREATE TABLE projeto (
    projnumero INT(10) PRIMARY KEY,
    projnome VARCHAR(45),
    projlocalizacao VARCHAR(45),
    dnumero INT(10),
    FOREIGN KEY (dnumero) REFERENCES departamento(dnumero)
);

CREATE TABLE trabalha_em (
    cpf INT(10),
    projnumero INT(10),
    horas DOUBLE,
    PRIMARY KEY (cpf, projnumero),
    FOREIGN KEY (cpf) REFERENCES empregado(cpf),
    FOREIGN KEY (projnumero) REFERENCES projeto(projnumero)
);

CREATE TABLE depto_localizacoes (
    dlocalizacao VARCHAR(45),
    dnumero INT(10),
    PRIMARY KEY (dlocalizacao, dnumero),
    FOREIGN KEY (dnumero) REFERENCES departamento(dnumero)
);
