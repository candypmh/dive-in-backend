-- P18: Seoul pool license source tracking
-- Apply manually in the Supabase SQL Editor after review.

begin;

alter table pools
  add column if not exists source text not null default 'manual',
  add column if not exists external_id text,
  add column if not exists license_status text,
  add column if not exists license_date date,
  add column if not exists closed_date date,
  add column if not exists road_address text,
  add column if not exists lot_address text;

create unique index if not exists pools_source_external_id_uidx
  on pools (source, external_id)
  where external_id is not null;

commit;
