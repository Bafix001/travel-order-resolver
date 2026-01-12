import { Refine } from '@refinedev/core';
import { useNotificationProvider, ThemedLayout, ErrorComponent, RefineThemes } from '@refinedev/antd';
import "@refinedev/antd/dist/reset.css";
import { ConfigProvider, App as AntdApp } from "antd";
import { BrowserRouter, Route, Routes, Outlet } from "react-router";
import routerProvider, { NavigateToResource } from "@refinedev/react-router";
import { OrderList } from "./pages/orders/list";

// Data provider corrigé
const dataProvider = {
  getList: async () => {
    return Promise.resolve({
      data: [
        { id: 1, adresse: "DEPOT", type: "Base", ordre_passage: 0 },
        { id: 2, adresse: "r. d'Anjou", type: "Livraison", ordre_passage: 1 },
        { id: 3, adresse: "r. de la Harpe", type: "Livraison", ordre_passage: 2 },
        { id: 4, adresse: "r. Saint-Honoré", type: "Livraison", ordre_passage: 3 }
      ] as any,
      total: 4,
    });
  },
  getOne: async ({ id }: any) => {
    return Promise.resolve({
      data: { id: 1, adresse: "Test", type: "Test", ordre_passage: 0 } as any
    });
  },
  create: async ({ variables }: any) => {
    return Promise.resolve({ data: variables as any });
  },
  update: async ({ variables }: any) => {
    return Promise.resolve({ data: variables as any });
  },
  deleteOne: async ({ id }: any) => {
    return Promise.resolve({ data: { id } as any });
  },
  getApiUrl: () => "",
};

function App() {
  return (
    <BrowserRouter>
      <ConfigProvider theme={RefineThemes.Blue}>
        <AntdApp>
          <Refine 
            dataProvider={dataProvider as any}
            notificationProvider={useNotificationProvider}
            routerProvider={routerProvider}
            resources={[
              {
                name: "orders",
                list: "/orders",
              }
            ]}
            options={{
              syncWithLocation: true,
            }}
          >
            <Routes>
              <Route
                element={
                  <ThemedLayout>
                    <Outlet />
                  </ThemedLayout>
                }
              >
                <Route index element={<NavigateToResource resource="orders" />} />
                <Route path="/orders" element={<OrderList />} />
              </Route>
              <Route path="*" element={<ErrorComponent />} />
            </Routes>
          </Refine>
        </AntdApp>
      </ConfigProvider>
    </BrowserRouter>
  );
}

export default App;