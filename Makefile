exec: Benchmark.py Entradas.entry
	@python3 Benchmark.py < Entradas.entry

kill: KillThem.py
	@python3 KillThem.py
	@rm top.txt

clean:
	@rm -r Logs Results
	@rm *.txt
