with anime_characters as (
    select * from {{ ref('anime_characters') }}
)
select distinct
    {{ dbt_utils.generate_surrogate_key(['ac.character_id', 'ac.anime_id']) }} as id,
    ac.character_id,
    ac.anime_id,
    ac.character_external_id,
    ac.anime_external_id,
    ac.media_type,
    ac.character_name,
    replace(ac.character_image, '.jpg-thumb', '') as character_image,
    ac.character_type,
    ac.character_rating,
    ac.anime_title,
    ac.anime_title_secondary,
    ac.anime_image,
    ac.trash,
    ac.waifu,
    ac.anime_popularity,
    ac.anime_favorited,
    ac_desc.description as character_description
from anime_characters ac 
inner join {{ ref('src_character_desc') }} ac_desc on ac.character_external_id = ac_desc.external_id
and ac_desc.description is not null
