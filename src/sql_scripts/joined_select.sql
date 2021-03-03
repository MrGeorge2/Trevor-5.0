SELECT 
	TCandleApi.id,
	TCandleApi.symbol,
	TCandleApi.open_time,
	TCandleApi.open_price,
	TCandleApi.high_price,
	TCandleApi.low_price,
	TCandleApi.close_price,
	TCandleApi.volume,
	TResults.up,
	TResults.down


FROM TCandleApi

INNER JOIN TResults
	ON TCandleApi.symbol=TResults.symbol
	AND TCandleApi.open_time=TResults.open_time