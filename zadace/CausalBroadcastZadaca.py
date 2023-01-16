import asyncio


NODES = 3

delivered = [0] * NODES # [0, 0, 0]
buffer = {}

async def onReceive(reader, _):
	"""
	Handle TCP message
	"""
	while data := await reader.read(100):
		try:
			ldata = data.decode("utf8").split(",", maxsplit=2)
			sender, seq, msg = int(ldata[0]), int(ldata[1]), ldata[2].strip()

			print("Received:", sender, seq, msg)
			buffer[sender, seq] = msg

			# deps, deps[sender] = delivered, seq

			# find a message to deliver
			def deliverMessage():
					print(f"Status: ", "-".join(map(str, delivered)))
					for n, x in enumerate(delivered):
						if (n, x) in buffer: # and deps <= delivered
							print(f"*** Delivering (node={n}, seq={x}):", buffer[n, x])
							del buffer[n, x] # ?
							delivered[n] += 1
							return True

			while deliverMessage():
					pass

		except Exception as e:
			print(e)


async def main():
	server = await asyncio.start_server(onReceive, "127.0.0.1", 9000)

	print(server.sockets)

	async with server:
		await server.serve_forever()


asyncio.run(main())
