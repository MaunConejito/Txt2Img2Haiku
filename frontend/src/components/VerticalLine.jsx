import { Center } from '@chakra-ui/react';

export default function VerticalLine({
  length,
  width,
  color,
  lineStyle,
  ...props
}) {

  const style = {
    width: '0px',
    height: length ?? '50px',
    borderWidth: '0px',
    borderLeftWidth: width ?? '3px',
    color: color ?? 'gray.200',
    borderStyle: lineStyle ?? 'solid'
  }

  return(
    <Center>
      <div
      style={style}
      {...props}/>
    </Center>
  );
}
