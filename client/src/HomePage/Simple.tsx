import { useState } from 'react'
import styled from 'styled-components'

type SimpleProps = {
    defaultState: number;
}

const Simple = (props: SimpleProps) => {
    const [counter, updateCounter] = useState(props.defaultState)

    const handleClick = () =>  {
        updateCounter(counter + 100000)
    }

    return (
        <div onClick = { handleClick }>
            <div>current count</div>
            <div>{ counter }</div>
        </div>
    )
}

export default Simple

const Title = styled.div`
    background-color: black;
    font-size: 100px
`