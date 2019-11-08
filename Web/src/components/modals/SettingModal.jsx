import Modal from "react-bootstrap/Modal";
import React, { useState, useEffect } from "react";
import axios from "axios";

function SettingModal(props) {
  const [opponents, setOpponents] = useState([]);
  const { setOpponent } = props;
  useEffect(() => {
    axios
      .get(
        `http://${window.location.hostname}:${window.location.port}/ai/game/v1.0`
      )
      .then(res => {
        setOpponents(res.data.opponents);
        setOpponent(res.data.opponents[0]);
      });
  }, [setOpponent]);

  return (
    <>
      <Modal
        size="lg"
        show={props.showSettings}
        onHide={() => {
          props.dealCards();

          props.setShowSettings(false);
        }}
        aria-labelledby="example-modal-sizes-title-lg"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-modal-sizes-title-lg">
            {"Settings"}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <select
            onChange={event => {
              props.setOpponent(event.target.value);
            }}
          >
            {opponents.map(opponent => {
              return (
                <option key={opponent} value={opponent}>
                  {opponent}
                </option>
              );
            })}
          </select>
        </Modal.Body>
      </Modal>
    </>
  );
}

export default SettingModal;