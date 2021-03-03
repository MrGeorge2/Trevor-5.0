CREATE VIEW IF NOT EXISTS  VJoinedVRes as
SELECT
    TCandleApi.id,
	TCandleApi.symbol,
	TCandleApi.open_time,
	TCandleApi.open_price,
	TCandleApi.high_price,
	TCandleApi.low_price,
	TCandleApi.close_price,
	TResults.up,
	TResults.down,
	TResults.train


FROM TCandleApi

INNER JOIN TResults
	ON TCandleApi.symbol=TResults.symbol
	AND TCandleApi.open_time=TResults.open_time;