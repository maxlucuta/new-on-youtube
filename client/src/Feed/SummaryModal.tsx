import { Dispatch, SetStateAction } from "react";
import styled from "styled-components";
import { Summary } from "../types";
import { thumbnail } from "../functions";
import { url } from "../functions";

type SummaryModalProps = {
    updateSummaryModalOpen: Dispatch<SetStateAction<boolean>>;
    summary: Summary;
};

const SummaryModal = (props: SummaryModalProps) => {
    return (
        <Container onClick={() => props.updateSummaryModalOpen(false)}>
            <Modal>
                <Title>{props.summary.title}</Title>
                <div style={{ textAlign: "center" }}>
                    <a href={url(props.summary.id)}>
                        <Img src={thumbnail(props.summary.id)} />
                    </a>
                </div>
                <div style={{ textAlign: "center", fontSize: "10px" }}>click to visit!</div>
                <Description>{props.summary.description}</Description>
            </Modal>
        </Container>
    );
};

export default SummaryModal;

const Container = styled.div`
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vw;
    background-color: rgba(0, 0, 0, 0.5);
`;

const Modal = styled.div`
    position: fixed;
    top: 0;
    width: 50%;
    height: 50%;
    margin: 250px 25vw;
    background-color: white;
    color: black;
    border-radius: 10px;
`;

const Img = styled.img`
    border-radius: 10px;
    width: 40%;
`;

const Description = styled.div`
    text-align: center;
    width: 85%;
    font-size: 15px;
    margin: 20px auto;
`;

const Title = styled.div`
    text-align: center;
    width: 85%;
    font-size: 20px;
    margin: 20px auto;
`;
