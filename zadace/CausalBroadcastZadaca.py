import asyncio


NODES = 5
delivered = [0] * NODES # [0, 0, 0, 0, 0]
buffer = {}

async def onReceive(reader, _):
	"""
	Handle TCP message
	"""
	print("New connection received / made.\n")
	while data := await reader.read(100):
		try:
			ldata = data.decode("utf8").split(",", maxsplit=2)
			sender, vectorClock, msg = int(ldata[0]), tuple(map(int, ldata[1].strip('[]').split('-'))), ldata[2].strip()

			print("Received:", sender, vectorClock, msg)
			buffer[sender, vectorClock] = msg

			# find a message to deliver
			def deliverMessage():
				print(f"Status: ", "-".join(map(str, delivered)))
				for (n, x), m in buffer.items():
					if all(True if x[node] <= delivered[node] else False for node in range(NODES)):
						print(f"*** Delivering (node = {n}, deps = {x}, message = '{m}'):")
						del buffer[n, x]
						delivered[n] += 1
						return True
			
			while deliverMessage():
					pass

			print()

		except Exception as e:
			print(e)


async def main():
	server = await asyncio.start_server(onReceive, "127.0.0.1", 9000)

	print(server.sockets)

	async with server:
		await server.serve_forever()


asyncio.run(main())

"""
0,[0-0-0-0-0],Hello there!
1,[1-0-0-0-0],General Kenobi... 
2,[1-2-0-0-0],This is star trek
1,[1-0-0-0-0],Is this star wars?

New connection received / made.
Received: 0 (0, 0, 0, 0, 0) Hello there!
Status:  0-0-0-0-0
*** Delivering (node = 0, deps = (0, 0, 0, 0, 0), message = 'Hello there!'):
Status:  1-0-0-0-0

Received: 1 (1, 0, 0, 0, 0) General Kenobi...
Status:  1-0-0-0-0
*** Delivering (node = 1, deps = (1, 0, 0, 0, 0), message = 'General Kenobi...'):
Status:  1-1-0-0-0

Received: 2 (1, 2, 0, 0, 0) This is star trek
Status:  1-1-0-0-0

Received: 1 (1, 0, 0, 0, 0) Is this star wars?
Status:  1-1-0-0-0
*** Delivering (node = 1, deps = (1, 0, 0, 0, 0), message = 'Is this star wars?'):
Status:  1-2-0-0-0
*** Delivering (node = 2, deps = (1, 2, 0, 0, 0), message = 'This is star trek'):
Status:  1-2-1-0-0


"""
