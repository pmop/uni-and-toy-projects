
with basequery as (
    select z.ClientID, sum(z.Handle) as Handle
    from (
    select ClientID, sum(BetAmountNative) as Handle
    from vwsports s
    where BetPrice >= .5
    and BetDatePSTKey >= 20230705
    and ComboSingle = 'single'
	and eventtype in ('nfl','cfl')
    group by ClientID

    union

select ClientID, sum(BetAmountNative) as Handle
	from vwsports s
	inner join (select combinationid
	from vwSports
	where eventtype in ('nfl','cfl')
	and BetDatePSTKey >= 20230705
	and ComboSingle = 'combo'
	and CombinationPrice >= .5
	group by CombinationID)v on v.CombinationID = s.CombinationID

	group by clientid, BetDatePSTKey



) as Z
group by z.ClientID )

select b.ClientID, b.Handle AS CumulativeHandle  , case when b.handle > 2500 then 100 else  Floor( b.handle/50 ) * 2 end as Bankroll
from basequery b
inner join ClientGroupMembers cgm on b.clientid = cgm.ClientID


Group by b.ClientID,b.handle , case when b.handle > 2500 then 100 else  Floor( b.handle/50 ) * 2 end
