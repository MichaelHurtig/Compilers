program example;
var ans: real;
function fib(num: integer): integer;
begin
	if (num = 0) then
		fib := 0
	else if (num = 1) then
		fib := 1
	else
		fib := fib(num - 1) + fib(num - 2)
end;
begin
	ans := fib(9);
	write	ans
end.

