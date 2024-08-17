with raw_anime as (
    select * from {{ source('anime_db', 'anime') }}
)
select 
    id,
    external_id,
    image as image_src,
    title,
    award,
    type as anime_type,
    episodes,
    case
        when rating like 'N/A%' then null
        else nullif(split_part(rating, ' ', 1), '')::float
    end as rating,
    case 
        when rating like 'N/A%' then null
        else nullif(nullif(split_part(split_part(rating, '(', 2), ')', 1), ''), 'N/A (0)')::int
    end as total_ratings,
    case
        when average like 'N/A%' then null
        else nullif(split_part(average, ' ', 1), '')::float
    end as average,
    case 
        when average like 'N/A%' then null
        else nullif(nullif(split_part(split_part(average, '(', 2), ')', 1), ''), 'N/A (0)')::int
    end as total_average,
    case
        when reviews like 'N/A%' then null
        else nullif(split_part(reviews, ' ', 1), '')::float
    end as reviews,
    case 
        when reviews like 'N/A%' then null
        else nullif(nullif(split_part(split_part(reviews, '(', 2), ')', 1), ''), 'N/A (0)')::int
    end as total_reviews,
    users,
    case 
        when position('?' in aired) > 0 then null
        else 
            case 
                when aired is null or aired = '' then null
                when aired != '-' then to_date(aired, 'fmdd.fmmm.yyyy')::timestamp
                else null
            end
    end as aired_date,
    case 
        when position('?' in ended) > 0 then null
        when ended != '-' then to_date(ended, 'fmdd.fmmm.yyyy')::timestamp
        else null
    end as ended_date,
    CAST(regexp_replace(popularity, '\#', '') AS INT) as popularity,
    CAST(regexp_replace(favorites, '\#', '') AS INT) as favorited
from raw_anime