local frandom = io.open("/dev/urandom", "rb")
local frandom = io.open("/dev/urandom", "rb")
local d = frandom:read(4)
math.randomseed(d:byte(1) + (d:byte(2) * 256) + (d:byte(3) * 65536) + (d:byte(4) * 4294967296))

number =  math.random(1001,3000)
request = function()
    headers = {}
    headers["Content-Type"] = "application/json"
    body = ''
    return wrk.format("GET", "/conference_users/find/".. tostring(number), headers, body)
end