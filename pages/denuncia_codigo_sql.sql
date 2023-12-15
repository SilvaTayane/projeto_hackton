CREATE table pessoa(
	id_pessoa integer PRIMARY key AUTOINCREMENT,
	nome_completo text,
	cpf TEXT
);

create table denuncia(
	id_denuncia INTEGER PRIMARY key AUTOINCREMENT,
	comentario text,
	tipo_denuncia text
);

CREATE table local(
	id_local INTEGER PRIMARY key AUTOINCREMENT,
	endereco text,
	coordenadas INTEGER,
	ponto_de_referencia text
);

CREATE table faz(
	id_faz INTEGER PRIMARY key AUTOINCREMENT,
	id_pessoa INTEGER,
	id_denuncia INTEGER,
	FOREIGN key(id_pessoa) REFERENCES pessoa(id_pessoa),
	FOREIGN key(id_denuncia) REFERENCES denuncia(id_denuncia)
)	

CREATE table pertence(
	id_pertence INTEGER PRIMARY key AUTOINCREMENT,
	id_local INTEGER,
	id_denuncia INTEGER,
	FOREIGN key(id_local) REFERENCES local(id_local),
	FOREIGN key(id_denuncia) REFERENCES denuncia(id_denuncia)
)	