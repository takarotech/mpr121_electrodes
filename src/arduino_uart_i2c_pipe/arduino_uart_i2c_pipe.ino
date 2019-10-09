/*
 * UART (Serial) to I2C (Wire) pipe, with simple hexlified protocol:
 * read_size (0 = write), slave_address, [value1, value2..], '\n'
 * Arad Eizen 08/10/19.
 */

/* Output debug messages via this pin if defined */
#define UART_DEBUG_TX_PIN		(9)


#if defined(UART_DEBUG_TX_PIN)
	#include <SoftwareSerial.h>
	SoftwareSerial debug(-1, UART_DEBUG_TX_PIN);
	#define DEBUG_PRINT(s)		debug.print(s)
#else
	#define DEBUG_PRINT(s)
#endif

#include <Wire.h>
#include "hex_utils.h"

#define UART_BAUD_RATE			(115200)
#define UART_TIMEOUT			(100)
#define UART_TERMINATOR			'\n'
#define UART_BUFFER_SIZE		(128)
#define I2C_BUFFER_SIZE			(UART_BUFFER_SIZE / 2)


char uart_buffer[UART_BUFFER_SIZE];
uint8_t i2c_buffer[I2C_BUFFER_SIZE];


void setup(void)
{
	/* Initialize debug UART if needed */
#if defined(UART_DEBUG_TX_PIN)
	debug.begin(UART_BAUD_RATE);
	DEBUG_PRINT("\nstarted\n");
#endif

	/* Initialize UART */
	Serial.begin(UART_BAUD_RATE);
	Serial.setTimeout(UART_TIMEOUT);

	/* Initialize I2C */
	Wire.begin();
}

void loop(void)
{
	size_t size;
	uint8_t address;

	if (size = Serial.readBytesUntil(UART_TERMINATOR, uart_buffer, UART_BUFFER_SIZE)) {
#if defined(UART_DEBUG_TX_PIN)
		uart_buffer[size] = '\0';
		DEBUG_PRINT("uart: read(");
		DEBUG_PRINT(size);
		DEBUG_PRINT(") -> \"");
		DEBUG_PRINT(uart_buffer);
		DEBUG_PRINT("\"\n");
#endif
		switch (unhexlify(uart_buffer, i2c_buffer, size)) {
		case ERR_OK:
			address = i2c_buffer[0];

			if (i2c_buffer[1]) {
				size = i2c_buffer[1];

				DEBUG_PRINT("i2c: request(");
				DEBUG_PRINT(size);
				DEBUG_PRINT(") -> ");
				Wire.requestFrom(address, size);

				size = 0;
				while (Wire.available())
					i2c_buffer[size++] = Wire.read();

				DEBUG_PRINT(size);
				DEBUG_PRINT('\n');

				hexlify(i2c_buffer, uart_buffer, size);

				Serial.print(uart_buffer);
				Serial.print(UART_TERMINATOR);

				DEBUG_PRINT("\nuart: write(");
				DEBUG_PRINT(size * 2);
				DEBUG_PRINT(") -> \"");
				DEBUG_PRINT(uart_buffer);
				DEBUG_PRINT("\"\n");
			}
			else {
				size /= 2;

				DEBUG_PRINT("i2c: write(");
				DEBUG_PRINT(size - 2);
				DEBUG_PRINT(")\n");
				Wire.beginTransmission(address);

				for (size_t i = 2; i < size; i++)
					Wire.write(i2c_buffer[i]);

				Wire.endTransmission();
			}
			break;
		case ERR_ODD_LENGTH:
			DEBUG_PRINT("unhexlify error: odd length string\n");
			break;
		case ERR_INVALID_CHARACTER:
			DEBUG_PRINT("unhexlify error: invalid character\n");
			break;
		}
	}
}
