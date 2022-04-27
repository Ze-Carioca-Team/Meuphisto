import React from "react";
import ReactDOM from "react-dom/client";

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Grid from '@mui/material/Grid';
import { ChatApp, ChatMessage } from "bootstrap-chat";
import Store from "global-context-store";
import { AppShell, Layer, VideoPlayer } from "annotation-toolkit";

import "annotation-toolkit/build/main.css";
import "@blueprintjs/core/lib/css/blueprint.css";

import { useMephistoTask } from "mephisto-task";

function Task(){
  const {
      taskConfig,
      agentId,
      assignmentId,
      initialTaskData,
      handleSubmit,
      isLoading,
      isOnboarding,
      isPreview,
      previewHtml,
      blockedReason
  } = useMephistoTask();
  return(
    <div>
      Hey
    </div>
  )
}

function Chat(){
  return(
    <div style={{height: "60vh", width: "60vw"}}> 
      <ChatApp
        renderMessage={({ message }) => <ChatMessage message={message.text + "!!!!!"} />}
      />
    </div>
  )
}

function Toolkit(){
  return(
    <div style={{height: "60vh", width: "60vw"}}> 
      <Store>
        <AppShell layers={() => {
          return (
            <Layer
              displayName="Video"
              icon="video" /* uses blueprintjs icons: https://blueprintjs.com/docs/#icons */
              component={({ id }) => (
                <VideoPlayer
                  fps={30}
                  id={id}
                  src="https://www.youtube.com/watch?v=zw0BfYNPlbU"
                  scale={0.5}
                />
              )}
            />
          )}} />
      </Store>
    </div>
  )
}

function Main(){
  const [tab, setTab] = React.useState(0);
  return(
    <Grid container direction="column" justifyContent="center" alignItems="center">
      <Grid item>
        <Tabs value={tab} onChange={(event, ntab)=>setTab(ntab)}>
          <Tab label="Mephisto Task" />
          <Tab label="Bootstrap-Chat"/>
          <Tab label="Annotation-Toolkit"/>
          <Tab label="Mephisto-Review"/>
        </Tabs>
      </Grid>
      <Grid item>
        {/* <Chat /> */}
        {/* <Toolkit /> */}
        {/* <Task /> */}
      </Grid>
    </Grid>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<Main />);