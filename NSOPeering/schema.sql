drop table if exists devices;
drop table if exists prefixset;
drop table if exists routepolicy;
drop table if exists prefix;

PRAGMA foreign_keys = ON;

create table devices (
  device text not null primary key,
  ipAddress text not null unique
);

create table prefixset (
  prefixset text not null primary key,
  device text not null,
  foreign key (device) references devices(device)
);

create table routepolicy (
  routepolicy text not null,
  prefixset text not null,
  foreign key (prefixset) references prefixset(prefixset)
);

create table prefix (
  device text not null,
  prefixset text not null,
  foreign key (device) references devices(device),
  foreign key (prefixset) references prefixset(prefixset)
);
