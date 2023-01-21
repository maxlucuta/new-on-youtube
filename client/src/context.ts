import { createContext } from "react"

type RootContextType = {
    SERVER_URL: string;
}

export const RootContext = createContext<RootContextType>({ SERVER_URL: "" })