drop table if exists devices;
drop table if exists prefixsets;
drop table if exists routepolicys;
drop table if exists prefixes;

PRAGMA foreign_keys = ON;

create table devices (
  device text not null primary key,
  ipAddress text not null unique
);

create table prefixsets (
  prefsetId integer primary key autoincrement,
  prefixset text not null,
  device text not null,
  foreign key (device) references devices(device)
);

create table routepolicys (
  routepolicy text not null,
  prefixset text not null,
  foreign key (prefixset) references prefixsets(prefixset)
);

create table prefixes (
  prefId integer primary key autoincrement,
  prefsetId integer,
  prefix text,
  mask text,
  foreign key (prefsetId) references prefixsets(prefsetId)
);
