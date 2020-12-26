

select urls.id, url, error
from errors join urls on urls.id = errors.url_id
order by urls.id desc;
