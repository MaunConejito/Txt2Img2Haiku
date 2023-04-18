import { useState, useEffect } from 'react';

import { SimpleGrid, Box, Center, Image, Spinner } from '@chakra-ui/react'

export default function ImgDisplay({ imgs, waiting }) {
  const [text, setText] = useState('');

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
        {imgs.map((img, i) =>
          <Center
          m='10px'>
            <Image
            src={'/data/imgs/'+img}
            key={i}
            borderRadius='10'/>
          </Center>
        )}
      </SimpleGrid>
    )
  );
}
