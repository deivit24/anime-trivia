with raw_character as (
    select * from {{ source('anime_db', 'character') }}
)
select
    id,
    external_id,
    image as image_src,
    name,
    type as character_type,
    anime_appearance as anime,
    age,
    case 
        when gender != '-' then gender
        else null
    end as gender,
    case 
        when blood_type != '-' then blood_type
        else null
    end as blood_type,
    dob,
    case
        when rating like 'N/A%' then null
        else nullif(split_part(rating, ' ', 1), '')::float
    end as rating,
    case 
        when rating like 'N/A%' then null
        else nullif(nullif(split_part(split_part(rating, '(', 2), ')', 1), ''), 'N/A (0)')::int
    end as total_ratings,
    waifu,
    trash
from raw_character