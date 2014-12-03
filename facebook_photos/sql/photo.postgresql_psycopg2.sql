--facebook_photos_photo_likes_users

CREATE UNIQUE INDEX facebook_photos_photo_likes_users_time_from_3col_uniq
ON facebook_photos_photo_likes_users (photo_id, user_id, time_from)
WHERE time_from IS NOT NULL;

CREATE UNIQUE INDEX facebook_photos_photo_likes_users_time_from_2col_uniq
ON facebook_photos_photo_likes_users (photo_id, user_id)
WHERE time_from IS NULL;

CREATE UNIQUE INDEX facebook_photos_photo_likes_users_time_to_3col_uniq
ON facebook_photos_photo_likes_users (photo_id, user_id, time_to)
WHERE time_to IS NOT NULL;

CREATE UNIQUE INDEX facebook_photos_photo_likes_users_time_to_2col_uniq
ON facebook_photos_photo_likes_users (photo_id, user_id)
WHERE time_to IS NULL;

--facebook_photos_photo_shares_users

CREATE UNIQUE INDEX facebook_photos_photo_shares_users_time_from_3col_uniq
ON facebook_photos_photo_shares_users (photo_id, user_id, time_from)
WHERE time_from IS NOT NULL;

CREATE UNIQUE INDEX facebook_photos_photo_shares_users_time_from_2col_uniq
ON facebook_photos_photo_shares_users (photo_id, user_id)
WHERE time_from IS NULL;

CREATE UNIQUE INDEX facebook_photos_photo_shares_users_time_to_3col_uniq
ON facebook_photos_photo_shares_users (photo_id, user_id, time_to)
WHERE time_to IS NOT NULL;

CREATE UNIQUE INDEX facebook_photos_photo_shares_users_time_to_2col_uniq
ON facebook_photos_photo_shares_users (photo_id, user_id)
WHERE time_to IS NULL;
