import { useState, useEffect, useContext } from 'react';

import { Center, Container, Spinner } from '@chakra-ui/react';

import { ConfigContext } from '../App.jsx';
import HaikuDisplay from './HaikuDisplay.jsx';

export default function HaikuFinder({ query, n }) {
  const config = useContext(ConfigContext);
  const [haikus, setHaikus] = useState(null);

  const extractHaikuList = (resultJson) => {
    return resultJson.results.map((r) => r.payload.lines);
  };

  useEffect(() => {
    setHaikus(null);
    fetch(config.serviceUrl + '/api/haiku/search?n=' + n, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(query)
    })
    .then((response) => response.json())
    .then(
      (json) => {
        setHaikus(extractHaikuList(json));
      },
      (error) => {
        console.error("Haiku request failed: " + error.message);
        setHaikus(null);
      }
    );
  }, [query, config, n])

  return (
    <Container
    maxW='xl'
    centerContent
    border='2px'
    borderColor='gray.300'
    bg='gray.50'
    borderRadius='20px'
    boxShadow='md'>
      {haikus ? (
        <HaikuDisplay
        haikus={haikus}/>
      ) : (
        <Center>
          <Spinner
          size='xl'
          m='20px'/>
        </Center>
      )}
    </Container>
  );
}
