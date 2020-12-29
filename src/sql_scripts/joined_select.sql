SELECT 
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
	TResults.up,
	TResults.down
	
FROM TCandleApi INNER JOIN TResults 
	ON TCandleApi.symbol=TResults.symbol 
	AND TCandleApi.open_time=TResults.open_time;