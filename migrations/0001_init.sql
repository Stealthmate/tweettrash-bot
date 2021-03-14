CREATE TABLE IF NOT EXISTS tweets (
  tweet_id TEXT PRIMARY KEY,
  created_at INT NOT NULL,
  username TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS members (
  username TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  profile_img_url TEXT
);
