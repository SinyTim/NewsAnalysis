

drop function if exists get_generation_last_state;

create function get_generation_last_state(source_ varchar(256))
returns varchar(256) as $$
    select stop_state
    from url_generation
    where id = (
        select max(id)
        from url_generation
        where (source = source_) and (stop_state is not null)
    );
$$ language sql;


drop function if exists start_url_generation;

create function start_url_generation(source_ varchar(256), start_state_ varchar(256))
returns bigint as $$
    insert into url_generation (source, start_state)
    values (source_, start_state_)
    returning id;
$$ language sql;


drop function if exists stop_url_generation;

create function stop_url_generation(url_generation_id_ bigint, stop_state_ varchar(256))
returns void as $$
    update url_generation set
        stop_state = stop_state_,
        stop_time = now()
    where id = url_generation_id_;
$$ language sql;


--drop function if exists get_unprocessed_urls;
--
--create function get_unprocessed_urls(process_name_ varchar(256))
--returns table(url_id bigint, url varchar(256), source varchar(256)) as $$
--    with
--    cte_processed_ids as (
--        select distinct url_id
--        from url_audit
--        where (process_name = process_name_) and (stop_time is not null)
--    ),
--    cte_unprocessed as (
--        select urls.*
--        from urls left join cte_processed_ids
--        on urls.id = cte_processed_ids.url_id
--        where cte_processed_ids.url_id is null
--    )
--    select
--        cte_unprocessed.id,
--        cte_unprocessed.url,
--        url_generation.source
--    from cte_unprocessed left join url_generation
--    on cte_unprocessed.url_generation_id = url_generation.id;
--$$ language sql;


--drop function if exists start_url_audit;
--
--create function start_url_audit(url_id_ bigint, destination_ varchar(256), process_name_ varchar(256))
--returns bigint as $$
--    insert into url_audit (url_id, destination, process_name)
--    values (url_id_, destination_, process_name_)
--    returning id;
--$$ language sql;
--
--
--drop function if exists stop_url_audit;
--
--create function stop_url_audit(audit_ids bigint[])
--returns void as $$
--    update url_audit set
--        stop_time = now()
--    where id in audit_ids;
--$$ language sql;
