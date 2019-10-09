#ifndef HEX_UTILS_H
#define HEX_UTILS_H

#include <Arduino.h>

#define INVALID_DEC		(16)
#define INVALID_HEX		'?'

enum {
	ERR_OK = 0,
	ERR_ODD_LENGTH,
	ERR_INVALID_CHARACTER,
};

/* hex character to nibble: 'b' -> 0xb */
uint8_t hex_to_dec(char c)
{
	if (c < '0')
		goto err_character;
	if (c <= '9')
		return c - '0';
	if (c < 'A')
		goto err_character;
	if (c <= 'F')
		return c - 'A' + 10;
	if (c < 'a')
		goto err_character;
	if (c <= 'f')
		return c - 'a' + 10;

err_character:
	return INVALID_DEC;
}

/* Parse nibble to hex character: 0xb -> 'b' */
char dec_to_hex(uint8_t c)
{
	if (c < 10)
		return c + '0';
	if (c < 16)
		return c + 'a' - 10;
	return INVALID_HEX;
}

/* Parse uint8_t buffer into hexlified string: [0x12, 0xab] -> "12ab" */
void hexlify(const uint8_t *src, char *dst, size_t size)
{
	uint8_t c;

	while (size--) {
		c = *src++;
		*dst++ = dec_to_hex(c >> 4);
		*dst++ = dec_to_hex(c & 15);
	}

	*dst = '\0';
}

/* Parse hexlified string into uint8_t buffer: "12ab" -> [0x12, 0xab] */
uint8_t unhexlify(const char *src, uint8_t *dst, size_t size)
{
	uint8_t c;
	bool msb = false;

	if (size % 2)
		return ERR_ODD_LENGTH;

	while (size--) {
		c = hex_to_dec(*src++);
		if (c >= INVALID_DEC)
			return ERR_INVALID_CHARACTER;

		if (msb)
			*dst++ |= c;
		else
			*dst = c * 16;

		msb = !msb;
	}

	return ERR_OK;
}

#endif
