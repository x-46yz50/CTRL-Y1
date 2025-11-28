local isLagging = false
if isLagging == false then
	isLagging = true
end

while true do
	if isLagging == true then
		for i = 1,27500 do
			print(math.sqrt(i))
		end
	end
end