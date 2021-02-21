

drop function if exists get_audit_last_state;

create function get_audit_last_state(process_name_ varchar(256))
returns varchar(256) as $$
    select state_stop
    from audit
    where id = (
        select max(id)
        from audit
        where (process_name = process_name_) and (state_stop is not null)
    );
$$ language sql;


drop function if exists start_audit;

create function start_audit(process_name_ varchar(256), state_start_ varchar(256))
returns bigint as $$
    insert into audit (process_name, state_start)
    values (process_name_, state_start_)
    returning id;
$$ language sql;


drop function if exists stop_audit;

create function stop_audit(audit_id_ bigint, state_stop_ varchar(256))
returns void as $$
    update audit set
        state_stop = state_stop_,
        time_stop = now()
    where id = audit_id_;
$$ language sql;
