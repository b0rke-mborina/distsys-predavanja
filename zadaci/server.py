import asyncio

async def handler(reader, writer):
	print("New connection!")

	writer.write(b"Hello!")
	await writer.drain()

	while True:
		l = await reader.readline()
		print(l.decode("utf-8"))
	
	return 

async def main():
	server = await asyncio.start_server(
		handler, "127.0.0.1", 8080 # funkcija koja ce zaprimati nove konekcije
	)

	print("Server started")

	async with server:
		await server.serve_forever()

asyncio.run(main())
