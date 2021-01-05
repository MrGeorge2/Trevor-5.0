CREATE VIEW IF NOT EXISTS  VJoinedVRes as
SELECT
    TCandleApi.id,
	TCandleApi.symbol,
	TCandleApi.open_time,
	TCandleApi.open_price,
	TCandleApi.high_price,
	TCandleApi.low_price,
	TCandleApi.close_price,
	TCandleApi.volume,
	TCandleApi.close_time,
	TCandleApi.quote_asset_volume,
	TCandleApi.number_of_trades,
	TCandleApi.taker_buy_base_asset_volume,
	TCandleApi.taker_buy_quote_asset_volume,
	TIndicators.sma21,
	TIndicators.sma200,
	TIndicators.ema21,
	TIndicators.ema200,
	TResults.up,
	TResults.down,
	TResults.train


FROM TCandleApi

INNER JOIN TResults
	ON TCandleApi.symbol=TResults.symbol
	AND TCandleApi.open_time=TResults.open_time

INNER JOIN TIndicators
	ON TCandleApi.symbol=TIndicators.symbol
	AND TCandleApi.open_time=TIndicators.open_time;