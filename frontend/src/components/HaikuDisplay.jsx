import { SimpleGrid, Stack, Text } from '@chakra-ui/react'

export default function HaikuDisplay({ haikus }) {
  return (
    <SimpleGrid
    columns={2}>
      {haikus?.map((haiku, i) =>
        <Stack
        key={i}
        m='10px'
        p='5px'
        border='1px'
        borderRadius='10px'
        borderColor='gray.300'>
          <Text key={i*3  } textAlign='center'>{haiku[0]}</Text>
          <Text key={i*3+1} textAlign='center'>{haiku[1]}</Text>
          <Text key={i*3+2} textAlign='center'>{haiku[2]}</Text>
        </Stack>
      )}
    </SimpleGrid>
  );
}
