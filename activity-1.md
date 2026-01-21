1. **What is caching and why is it important?**

 - Caching is the practice of temporarily storing freqently used data in a temporary high-speed storage layer like Ram or Memory. This makes the app to retrieve data instantly instead of fetcing from a slower data source such as a hard drive or database 

   The benefits of caching are : 
    - It is faster because reading from memory is faster than getting data from your database making your website seem to work instantly to the user 
    - It prevents your database from being overwhelmed by the same repetivitive requests and crashing during high website traffic 
    - By serving data from cache, you use less computing power and overal spend less cloud infrastructure costs.

2. **What are the different types of caching?**
 - Database query caching is saving the result of a specific SQL query
 - Template caching is saving a specific piece of HTML code within a page 
 - View caching is saving the entire output of a specific URL/Endpoint
 - Full-page caching is saving the entire HTTP response, often before the request even reaches Django

3. **Cache Invalidation Challenge**
 - The problem with caching is that there could be stale data whereby your cached data is different from the data in your database
 - Cache should be cleared based off time with TTL which is time to live whereby cached data is deleted after a set period automatically 
 - You can also delete or update the cache right after a write operation happens in the database such as Create, Update and Delete 