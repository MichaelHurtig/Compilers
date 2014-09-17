{test file}

program example;
var x, y: integer;
var z: array[ 1 .. 5 ] of real;
function gcd(a, b: integer): integer;
begin
    if b = 0 then gcd := a
    else gcd := gcd(b, a mod b)
end; 

begin
    read(x, y);
    write(gcd(x,y))
end.
