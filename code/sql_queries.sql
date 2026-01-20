


SELECT 
    ROUND(SUM(total_amount), 2) as total_revenue,
    ROUND(AVG(total_amount), 2) as avg_revenue_per_trip,
    COUNT(*) as total_trips
FROM trips;





SELECT 
    pickup_hour,
    COUNT(*) as trip_count,
    ROUND(AVG(trip_distance), 2) as avg_distance,
    ROUND(SUM(total_amount), 2) as hourly_revenue
FROM trips
GROUP BY pickup_hour
ORDER BY pickup_hour;





SELECT 
    pickup_day,
    COUNT(*) as trips,
    ROUND(SUM(total_amount), 2) as daily_revenue,
    ROUND(AVG(fare_amount), 2) as avg_fare
FROM trips
GROUP BY pickup_day
ORDER BY pickup_day;





SELECT 
    ROUND(pickup_latitude, 2) as zone_lat,
    ROUND(pickup_longitude, 2) as zone_lon,
    COUNT(*) as trip_count,
    ROUND(SUM(total_amount), 2) as zone_revenue
FROM trips
WHERE pickup_latitude BETWEEN 40.6 AND 40.85
  AND pickup_longitude BETWEEN -74.05 AND -73.75
GROUP BY 1, 2
ORDER BY trip_count DESC
LIMIT 10;





SELECT 
    pickup_weekday,
    COUNT(*) as trips,
    ROUND(AVG(total_amount), 2) as avg_fare,
    ROUND(AVG(trip_distance), 2) as avg_distance
FROM trips
GROUP BY pickup_weekday
ORDER BY 
    CASE pickup_weekday
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;





SELECT 
    CASE 
        WHEN trip_distance < 1 THEN '0-1 mi'
        WHEN trip_distance < 3 THEN '1-3 mi'
        WHEN trip_distance < 5 THEN '3-5 mi'
        WHEN trip_distance < 10 THEN '5-10 mi'
        ELSE '10+ mi'
    END as distance_bucket,
    COUNT(*) as trips,
    ROUND(AVG(fare_amount), 2) as avg_fare
FROM trips
GROUP BY 1
ORDER BY 
    CASE 
        WHEN distance_bucket = '0-1 mi' THEN 1
        WHEN distance_bucket = '1-3 mi' THEN 2
        WHEN distance_bucket = '3-5 mi' THEN 3
        WHEN distance_bucket = '5-10 mi' THEN 4
        ELSE 5
    END;





SELECT 
    CASE 
        WHEN pickup_hour BETWEEN 6 AND 11 THEN 'Morning'
        WHEN pickup_hour BETWEEN 12 AND 16 THEN 'Afternoon'
        WHEN pickup_hour BETWEEN 17 AND 20 THEN 'Evening'
        ELSE 'Night'
    END as time_period,
    COUNT(*) as trips,
    ROUND(SUM(total_amount), 2) as revenue,
    ROUND(AVG(tip_amount), 2) as avg_tip
FROM trips
GROUP BY 1
ORDER BY revenue DESC;





SELECT 
    passenger_count,
    COUNT(*) as trips,
    ROUND(AVG(total_amount), 2) as avg_fare,
    ROUND(AVG(trip_distance), 2) as avg_distance
FROM trips
WHERE passenger_count > 0 AND passenger_count <= 6
GROUP BY passenger_count
ORDER BY passenger_count;


