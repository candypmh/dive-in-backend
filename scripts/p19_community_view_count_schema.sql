-- P19: Community post view count tracking
-- Apply manually in the Supabase SQL Editor after review.

begin;

alter table public.communities
  add column if not exists view_cnt bigint not null default 0;

create or replace function public.increment_community_view_count(p_post_id bigint)
returns bigint
language plpgsql
set search_path = public
as $$
declare
  updated_view_cnt bigint;
begin
  update public.communities
  set view_cnt = view_cnt + 1
  where id = p_post_id
  returning view_cnt into updated_view_cnt;

  return updated_view_cnt;
end;
$$;

revoke execute on function public.increment_community_view_count(bigint)
from public, anon, authenticated;

grant execute on function public.increment_community_view_count(bigint)
to service_role;

commit;
