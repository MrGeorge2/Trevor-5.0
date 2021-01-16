CREATE VIEW IF NOT EXISTS  VJoinedVRes as
SELECT
    TCandleApi.id,
	TCandleApi.symbol,

	--- Prices
	TCandleApi.open_time,
	TCandleApi.open_price,
	TCandleApi.high_price,
	TCandleApi.low_price,
	TCandleApi.close_price,

	--- Binance indicators
	TCandleApi.volume,
	TCandleApi.close_time,
	TCandleApi.quote_asset_volume,
	TCandleApi.number_of_trades,
	TCandleApi.taker_buy_base_asset_volume,
	TCandleApi.taker_buy_quote_asset_volume,

    --- Volumes
    TIndicators.volume_adi,
    TIndicators.volume_obv,
    TIndicators.volume_cmf,
    TIndicators.volume_fi,
    TIndicators.volume_mfi,
    TIndicators.volume_em,
    TIndicators.volume_sma_em,
    TIndicators.volume_vpt,
    TIndicators.volume_nvi,
    TIndicators.volume_vwap,

    --- Volatility
    TIndicators.volatility_atr,
    TIndicators.volatility_bbm,
    TIndicators.volatility_bbh,
    TIndicators.volatility_bbl,
    TIndicators.volatility_bbw,
    TIndicators.volatility_bbp,
    TIndicators.volatility_bbhi,
    TIndicators.volatility_bbli,
    TIndicators.volatility_kcc,
    TIndicators.volatility_kch,
    TIndicators.volatility_kcl,
    TIndicators.volatility_kcw,
    TIndicators.volatility_kcp,
    TIndicators.volatility_kchi,
    TIndicators.volatility_kcli,
    TIndicators.volatility_dcl,
    TIndicators.volatility_dch,
    TIndicators.volatility_dcm,
    TIndicators.volatility_dcw,
    TIndicators.volatility_dcp,
    TIndicators.volatility_ui,

    --- Trend
    TIndicators.trend_macd,
    TIndicators.trend_macd_signal,
    TIndicators.trend_macd_diff,
    TIndicators.trend_sma_fast,
    TIndicators.trend_sma_slow,
    TIndicators.trend_ema_fast,
    TIndicators.trend_ema_slow,
    TIndicators.trend_adx,
    TIndicators.trend_adx_pos,
    TIndicators.trend_adx_neg,
    TIndicators.trend_vortex_ind_pos,
    TIndicators.trend_vortex_ind_neg,
    TIndicators.trend_vortex_ind_diff,
    TIndicators.trend_trix,
    TIndicators.trend_mass_index,
    TIndicators.trend_cci,
    TIndicators.trend_dpo,
    TIndicators.trend_kst,
    TIndicators.trend_kst_sig,
    TIndicators.trend_kst_diff,
    TIndicators.trend_ichimoku_conv,
    TIndicators.trend_ichimoku_base,
    TIndicators.trend_ichimoku_a,
    TIndicators.trend_ichimoku_b,
    TIndicators.trend_visual_ichimoku_a,
    TIndicators.trend_visual_ichimoku_b,
    TIndicators.trend_aroon_up,
    TIndicators.trend_aroon_down,
    TIndicators.trend_aroon_ind,
    TIndicators.trend_psar_up,
    TIndicators.trend_psar_down,
    TIndicators.trend_psar_up_indicator,
    TIndicators.trend_psar_down_indicator,
    TIndicators.trend_stc,

    --- Momentum
    TIndicators.momentum_rsi,
    TIndicators.momentum_stoch_rsi,
    TIndicators.momentum_stoch_rsi_k,
    TIndicators.momentum_stoch_rsi_d,
    TIndicators.momentum_tsi,
    TIndicators.momentum_uo,
    TIndicators.momentum_stoch,
    TIndicators.momentum_stoch_signal,
    TIndicators.momentum_wr,
    TIndicators.momentum_ao,
    TIndicators.momentum_kama,
    TIndicators.momentum_roc,
    TIndicators.momentum_ppo,
    TIndicators.momentum_ppo_signal,
    TIndicators.momentum_ppo_hist,
    TIndicators.others_dr,
    TIndicators.others_dlr,
    TIndicators.others_cr,

    --- Results
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