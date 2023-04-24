import { useState, useEffect } from 'react';

import { SimpleGrid, Box, Center, Image, Spinner } from '@chakra-ui/react'

export default function ImgDisplay({ urls, waiting }) {

  return (
    waiting ? (
      <Center>
        <Spinner
        size='xl'
        m='20px'/>
      </Center>
    ) : (
      <SimpleGrid
      minChildWidth={150}>
        {urls.map((url, i) =>
          <Center
          m='10px'>
            <Image
            src={url}
            fallbackSrc={'/fallback.webp'}
            key={i}
            borderRadius='10'/>
          </Center>
        )}
      </SimpleGrid>
    )
  );
}
