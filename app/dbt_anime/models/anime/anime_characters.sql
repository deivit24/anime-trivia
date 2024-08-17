with characters as (
    select * from {{ ref('src_characters') }}
),
anime as (
    select * from {{ ref('src_anime') }}
)
select
    {{ dbt_utils.generate_surrogate_key(['c.id', 'a.id']) }} as id,
    c.id as character_id,
    a.id as anime_id,
    c.external_id as character_external_id,
    a.external_id as anime_external_id,
    a.anime_type as media_type,
    c.name as character_name,
    c.image_src as character_image,
    c.character_type as character_type,
    c.rating as character_rating,
    a.title as anime_title,
    c.anime as anime_title_secondary,
    a.image_src as anime_image,
    c.trash,
    c.waifu,
    a.popularity as anime_popularity,
    a.favorited as anime_favorited
from characters c 
join anime a on a.title = c.anime
order by anime_popularity