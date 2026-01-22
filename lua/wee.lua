function wait(t)
    local start = os.time()
    repeat until os.time() > start + t
end

while true do
    print("\ninsira o seu salario:")
    io.write("> ")
    local input = io.read()
    local sal = tonumber(input)
    local rea = 0
    
    if sal == nil then
        print("entrada inválida. por favor, insira um número.")
    elseif sal >= 0 and sal <= 400 then
        rea = 0.15
        local per = rea * 100
        local nsal = sal + (sal * rea)
        local rea2 = nsal - sal
        print(string.format(" Novo salário: %.2f\n reajuste ganho: %.2f\n percentual de ajuste: %g%%", nsal, rea2, per))
        
    elseif sal >= 400.01 and sal <= 800 then
        rea = 0.12
        local per = rea * 100
        local nsal = sal + (sal * rea)
        local rea2 = nsal - sal
        print(string.format(" Novo salário: %.2f\n reajuste ganho: %.2f\n percentual de ajuste: %g%%", nsal, rea2, per))

    elseif sal >= 800.01 and sal <= 1200 then
        rea = 0.10
        local per = rea * 100
        local nsal = sal + (sal * rea)
        local rea2 = nsal - sal
        print(string.format(" Novo salário: %.2f\n reajuste ganho: %.2f\n percentual de ajuste: %g%%", nsal, rea2, per))

    elseif sal >= 1200.01 and sal <= 2000 then
        rea = 0.07
        local per = rea * 100
        local nsal = sal + (sal * rea)
        local rea2 = nsal - sal
        print(string.format(" Novo salário: %.2f\n reajuste ganho: %.2f\n percentual de ajuste: %g%%", nsal, rea2, per))

    elseif sal >= 2000.01 and sal <= 115490000000000.00 then
        rea = 0.04
        local per = rea * 100
        local nsal = sal + (sal * rea)
        local rea2 = nsal - sal
        print(string.format(" Novo salário: %.2f\n reajuste ganho: %.2f\n percentual de ajuste: %g%%", nsal, rea2, per))

    elseif sal >= 115490000000000.01 then
        print("mentiroso da porra mlk KKKKKKKKKKK")
        wait(1.5)
        while true do
            local chars = {}
            for i = 1, 80 do
                local val = math.random(1000000, 9999999) * math.sqrt(math.random(100, 900))
                chars[i] = string.char(math.floor(val % 26) + 65) 
            end
            print(table.concat(chars))
        end
    else
        print("entrada inválida. tente novamente.")
    end
end