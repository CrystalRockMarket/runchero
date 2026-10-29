-- Schema for Pokemon Top Movers. Idempotent.
CREATE TABLE IF NOT EXISTS card_prices (
  snap_date date NOT NULL DEFAULT CURRENT_DATE,
  card_id text NOT NULL,
  variant text NOT NULL,
  name text, set_name text, number text, rarity text,
  image_small text, image_large text,
  market numeric(10,2),
  tcg_updated text,
  PRIMARY KEY (snap_date, card_id, variant)
);
