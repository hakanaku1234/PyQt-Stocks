create table if not exists company (
	ticker text primary key,
	sic text not null references sector(sic),
	name text,
	addr1 text,
	addr2 text,
	city text,
	state text,
	zip text
);

create table if not exists sector (
	sic text primary key,
	name text
);

create table if not exists stock_price (
	ticker text,
    date text,
	open real,
	high real,
	low real,
	close real,
	adj_close real,
	volume real,
    primary key (ticker, date)
);
